from datetime import datetime, timedelta

startDate = datetime.now() - timedelta(365)
evalStartDate = startDate - timedelta(365)

stockTickerFileLocation = "../configuration_data/stock_list.txt"
configurationFileLocation = "../configuration_data/config.ini"

modelStoragePathBase = "../model_storage/{0}"
evaluationModelStoragePathBase = modelStoragePathBase.format("training/{0}")

LimitedNumericChangeSourceID = "LimitedNumericChangeCalculator"
MovementDirectionSourceID = "MovementDirectionCalculator"
PercentageChangesSourceID = "PercentageChangesCalculator"

VolumeMovementDirectionsSegmentedID = "VMDS"