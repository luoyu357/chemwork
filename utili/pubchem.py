import pubchempy as pcp

#https://pubchempy.readthedocs.io/en/latest/guide/introduction.html

class pubchem:

    def searchCompoundName(self, name):
        c = pcp.get_compounds(name, 'name')
        return self.parseCompound(c)

    def searchCompoundSmiles(self, smiles):
        c = pcp.get_compounds(smiles, 'smiles')
        return self.parseCompound(c)

    def parseCompound(self, compounds):
        result = []
        for compound in compounds:
            result.append({'formula':compound.molecular_formula, 'smiles':compound.isomeric_smiles})
        return result



if __name__ == '__main__':
    test = pubchem()
    a = test.searchCompoundSmiles('F[P-](F)(F)(F)(F)F.COC=1C2=C(C=CC1)N(C=1C=CC=C3[NH+](C4=CCC5=C(C4=C2C13)C=CC=C5)C)C')
    print(a)
    a = test.searchCompoundName("123")
    print(a)
