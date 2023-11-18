# ECO5037S_FinalExam
Algorand Python scripts

# Algorand atomic transfer using Algokit

Two accounts A and B. Account A send sends 5 Algos to account B and account B sends 2 units of an Algorand Standard Asset (ASA) to account A. 

Application Start: 

1. Account B is created, funded, then creates 1 ASA asset.
2. Account A is created funded, then opts into the assetID of the ASA held by Account B
3. An atomic TX is then made between accounts 

The Atomic Transfer is bundled as followed:

1. Account A Sends 5 Algo to Account B
2. Account B Sends 2 ASA to Account A