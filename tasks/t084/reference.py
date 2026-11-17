"""Pinned AlphaEvolve ring-loading reference, rationalized to denominator 84."""
def run_code():
    nums=[(75,5),(37,47),(41,35),(28,56),(22,20),(27,57),(62,12),(42,42),(12,62),(57,27),(20,22),(56,28),(35,41),(47,37),(5,75)]
    return {"pairs":[[f"{u}/84",f"{v}/84"] for u,v in nums]}
