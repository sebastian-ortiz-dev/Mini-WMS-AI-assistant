from fastapi import HTTPException, status
from models.bin_models import BinCreate, BinUpdateSchema
from repository.bins_repository import newBin, GetBins, updateBin


def createBin(data: BinCreate) -> str:
    code = get_or_generate_bin_code(data.aisle, data.bay, data.tier, data.position)
    change = newBin(data.aisle, data.bay, data.tier, data.position, code)

    if change == None:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    return "Bin created sucefully"

def listBin():
    bins = GetBins()

    if bins == None:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    return bins

def pathBin(data: BinUpdateSchema, bin_id: str) -> str:   
    code = get_or_generate_bin_code(data.aisle, data.bay, data.tier, data.position)
    change = updateBin(data.aisle, data.bay, data.tier, data.position, code, bin_id)

    if change == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error to process the data.")

    return 

def get_or_generate_bin_code(aisle: int, bay: str, tier: int, position: str) -> str:
  if bay == "string" or bay == None or position == "string" or position == None:
    return None
  
  return f"{aisle}-{bay.strip().upper()}-{tier}-{position.strip().upper()}"
