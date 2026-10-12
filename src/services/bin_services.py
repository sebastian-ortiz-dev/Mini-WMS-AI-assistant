from fastapi import HTTPException, status
from models.bin_models import BinCreate
from repository.bins_repository import newBin, GetBins


def createBin(data: BinCreate) -> str:
    code = get_or_generate_bin_code(data.aisle, data.bay, data.tier, data.position, data.generated_code)
    change = newBin(data.aisle, data.bay, data.tier, data.position, code)

    if change == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    return "Bin created sucefully"

def listBin():
   bins = GetBins()

   if bins == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

   return bins

def get_or_generate_bin_code(aisle: int, bay: str, tier: int, position: str, generated_code: str | None = None) -> str:
  if generated_code and generated_code.strip() and generated_code != "string":
    return generated_code.strip().upper()

  return f"{aisle}-{bay.strip().upper()}-{tier}-{position.strip().upper()}"
