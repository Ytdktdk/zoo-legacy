import random
from typing import Dict

class Gene:
    def __init__(self, name: str, dominant: str, recessive: str):
        self.__name = name
        self.__dominant = dominant
        self.__recessive = recessive
        self.__allele1 = dominant
        self.__allele2 = recessive
    @property
    def name(self) -> str:
        return self.__name
    @property
    def genotype(self) -> str:
        return f"{self.__allele1}{self.__allele2}"
    @property
    def phenotype(self) -> str:
        if self.__dominant in self.genotype.upper():
            return self.__dominant
        return self.__recessive
    def mutate(self, mutation_rate: float = 0.01):
        if random.random() < mutation_rate:
            if random.random() < 0.5:
                self.__allele1 = self.__dominant if self.__allele1 == self.__recessive else self.__recessive
            else:
                self.__allele2 = self.__dominant if self.__allele2 == self.__recessive else self.__recessive
    def __str__(self):
        return f"[{self.genotype}]"

class GeneticCode:
    def __init__(self, genes: Dict[str, Gene] = None):
        self.__genes = genes or {}
    def add_gene(self, gene: Gene):
        self.__genes[gene.name] = gene
    def get_gene(self, gene_name: str) -> Gene:
        if gene_name not in self.__genes:
            raise ValueError(f"Ген {gene_name} не найден")
        return self.__genes[gene_name]
    def get_all_genes(self) -> Dict[str, Gene]:
        return self.__genes.copy()
    def mutate_all(self, mutation_rate: float = 0.01):
        for gene in self.__genes.values():
            gene.mutate(mutation_rate)
    def combine(self, other):
        if set(self.__genes.keys()) != set(other.__genes.keys()):
            raise ValueError("Нельзя скрестить: разные наборы генов")
        new_genes = {}
        for gene_name in self.__genes:
            gene1 = self.__genes[gene_name]
            gene2 = other.__genes[gene_name]
            allele1 = random.choice([gene1._Gene__allele1, gene1._Gene__allele2])
            allele2 = random.choice([gene2._Gene__allele1, gene2._Gene__allele2])
            new_gene = Gene(gene_name, gene1._Gene__dominant, gene1._Gene__recessive)
            new_gene._Gene__allele1 = allele1
            new_gene._Gene__allele2 = allele2
            new_genes[gene_name] = new_gene
        return GeneticCode(new_genes)
    def __str__(self):
        return " ".join([str(gene) for gene in self.__genes.values()])
