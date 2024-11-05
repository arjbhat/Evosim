import copy
import random
from math import log2
from typing import Union

from evosim.constants import (
    INTERNAL_TYPE,
    MAX_WEIGHT,
    MIN_WEIGHT,
    MUTATION_RATE,
    NEURON_ID_BIT_LENGTH,
    NUM_INTERNAL_NEURONS,
)
from evosim.neuron.actions import ActionCommand, action_outputs
from evosim.neuron.internal import InternalCommand, internal_commands
from evosim.neuron.senses import SensoryCommand, sensory_commands
from evosim.utils import average_hex


class Gene:
    """
    TODO: update outdated comment
    A gene has neurons.
    """

    source: Union[SensoryCommand, InternalCommand]
    target: Union[ActionCommand, InternalCommand]
    weight: int

    def __init__(
        self,
        source: Union[SensoryCommand, InternalCommand],
        target: Union[ActionCommand, InternalCommand],
        weight: int,
    ):
        # The max weight is 32767, which is 16 bits
        if weight > MAX_WEIGHT:
            raise Exception(f"{weight} must be under {MAX_WEIGHT+1}")
        # The min weight is -32768, which is 16 bits
        if weight < MIN_WEIGHT:
            raise Exception(f"{weight} must be over {MIN_WEIGHT-1}")

        self.source = source
        self.target = target
        self.weight = weight

    def same_gene(self, gene: "Gene"):
        """Determine if the genes have the same source and target"""

        # need to implement better version of equality inside source and target
        return self.source == gene.source and self.target == gene.target

    def __repr__(self) -> str:
        return f"{self.source.label}->{self.target.label} {self.weight}"

    def bits_str(self) -> str:
        # Max bits required to store bits
        # max_source_bits = (len(list(sensory_commands)) - 1).bit_length()
        # max_target_bits = (len(list(action_outputs)) - 1).bit_length()
        num_bits = int(log2(MAX_WEIGHT + 1) + 1)

        source_index = self.source.id
        target_index = self.target.id

        # convert num_bits to 2s complement in binary
        two_comp = lambda n: format(n & ((1 << num_bits) - 1), f"0{num_bits}b")

        source_type = 1 if self.source.type == INTERNAL_TYPE else 0
        target_type = 0 if self.target.type == INTERNAL_TYPE else 1

        return f"{source_type:01b}{source_index:0{NEURON_ID_BIT_LENGTH}b}{target_type:01b}{target_index:0{NEURON_ID_BIT_LENGTH}b}{two_comp(self.weight)}"

    @staticmethod
    def process_binary(binary_str):
        """
        Convert binary string to two's complement integer, take the absolute value,
        and convert it back to binary with specified bit length.
        """
        # Convert to integer assuming two's complement representation
        int_val = int(binary_str, 2)
        if binary_str[0] == "1":  # if the binary number is negative
            int_val -= 2 ** len(binary_str)

        # Convert absolute value back to binary
        abs_binary = bin(abs(int_val))[2:]

        # Pad with zeros to the specified bit length using zfill, if provided
        res = abs_binary.zfill(len(binary_str))

        if res[0] == "1":
            return "0" + "1" * (len(binary_str) - 1)
        return res

    def to_hex(self):
        binary_representation = self.bits_str()
        source_binary_value = binary_representation[: NEURON_ID_BIT_LENGTH + 1]
        target_binary_value = binary_representation[NEURON_ID_BIT_LENGTH + 1 : (NEURON_ID_BIT_LENGTH + 1) * 2]
        weight_binary_value = binary_representation[(NEURON_ID_BIT_LENGTH + 1) * 2 :]

        # source red, target green, weight sign blue, weight magnitiude alpha
        source_hex = hex(int(source_binary_value, 2))[2:].zfill(2)
        target_hex = hex(int(target_binary_value, 2))[2:].zfill(2)

        # first convert to 2's complement, get integer value, find abs value, convert back to binary,
        # then convert to hex
        # weight_sign_hex = hex(int(weight_binary_value[0], 2) * 255)[2:].zfill(2)
        # Determine the weight sign and convert to hex
        if weight_binary_value[0] == "1":  # negative sign
            weight_sign = 255//2  # representing -1 in two's complement
        else:  # non-negative sign
            weight_sign = 0
        weight_sign_hex = hex(weight_sign)[2:].zfill(2)

        weight_mag_hex = hex(int(self.process_binary(weight_binary_value)[1:8], 2))[2:].zfill(2)

        rgba_color = f"#{source_hex}{target_hex}{weight_sign_hex}{weight_mag_hex}"

        return rgba_color

    def scale_weight(self):
        scale = (MAX_WEIGHT + 1) / 4
        return self.weight / scale

    @classmethod
    def random(cls) -> "Gene":
        return cls.str_to_gene(f"{random.randint(0, 2**32):032b}")

    @classmethod
    def str_to_gene(cls, s: str) -> "Gene":
        source_type = s[0] if NUM_INTERNAL_NEURONS > 0 else "0"
        target_type = s[NEURON_ID_BIT_LENGTH + 1] if NUM_INTERNAL_NEURONS > 0 else "1"
        source_id = int(s[1 : NEURON_ID_BIT_LENGTH + 1], 2)
        target_id = int(s[NEURON_ID_BIT_LENGTH + 2 : (NEURON_ID_BIT_LENGTH + 1) * 2], 2)
        if source_type == "0":
            source = SensoryCommand.get_class(source_id)()
        else:
            source = InternalCommand.get_class(source_id)
        if target_type == "1":
            target = ActionCommand.get_class(target_id)()
        else:
            target = InternalCommand.get_class(target_id)

        # Assuming s is a binary string, and we're looking at a specific slice
        binary_string = s[(NEURON_ID_BIT_LENGTH + 1) * 2 :]

        # Convert the binary string to an integer
        binary_int = int(binary_string, 2)

        # Convert the integer to a signed integer using 2 bytes
        # We use 2 bytes because the maximum length of the binary string is 16 bits
        weight = int.from_bytes(
            binary_int.to_bytes(2, byteorder="big", signed=False),
            byteorder="big",
            signed=True,
        )

        return cls(source, target, weight)

    def to_mutated(self) -> "Gene":
        bits = self.bits_str()
        bit_list = list(bits)
        random_index = random.randint(0, len(bit_list) - 1)
        # Switch bit
        bit_list[random_index] = "1" if bit_list[random_index] == "0" else "0"
        modified_bits = "".join(bit_list)

        return Gene.str_to_gene(modified_bits)


def no_cycles(genes: list[Gene], new_gene: Gene) -> bool:
    """
    Check if adding new_gene to genes would create a cycle, assuming genes are acyclic.
    """
    # Build a graph (as a dictionary) from the list of gene connections
    graph = {}
    for gene in genes:
        if gene.source.id in graph:
            graph[gene.source.id].add(gene.target.id)
        else:
            graph[gene.source.id] = {gene.target.id}

    # Function to check if there's a path from start to target
    def is_path(start, target, visited):
        if start == target:
            return True
        visited.add(start)

        for neighbour in graph.get(start, []):
            if neighbour not in visited:
                if is_path(neighbour, target, visited):
                    return True

        return False

    # Check if there's a path from new_gene[1] to new_gene[0]
    return not is_path(new_gene.target.id, new_gene.source.id, set())


class Genome:
    genes: list[Gene]

    def __init__(self, genes: list[Gene]):
        self.genes = genes

    def __iter__(self):
        return iter(self.genes)

    def __repr__(self) -> str:
        return f"[{', '.join(map(str, self.genes))}]"

    def to_hex(self):
        hex_colors = [gene.to_hex() for gene in self.genes]
        return average_hex(hex_colors)

    @classmethod
    def random(cls, num_connections: int) -> "Genome":
        genes = []
        while len(genes) < num_connections:
            new_gene = Gene.random()
            # Doesn't work because equality is checking instances that are different not the values
            if not any(new_gene.same_gene(gene) for gene in genes) and no_cycles(genes, new_gene):
                genes.append(new_gene)

        return Genome(genes)

    def to_mutated(self) -> "Genome":
        """
        Create a new genome based on the mutation rate
        There is a {MUTATION_RATE} chance of a mutation happening
        """

        if random.random() < MUTATION_RATE:
            return self

        genes = self.genes.copy()
        random.shuffle(genes)

        random_gene = genes.pop()

        retries = 0
        while True:
            if retries >= 5:
                break

            mutated_gene = random_gene.to_mutated()

            if no_cycles(genes, mutated_gene):
                genes.append(mutated_gene)
                break

            retries += 1

        return Genome(genes)
