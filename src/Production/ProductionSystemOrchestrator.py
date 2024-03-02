from src.Production.ProductuinSystemConfig import ProductionSystemConfig
from src.Production.ProductionSystemPhaseTracker import ProductionSystemPhaseTracker
# Get an instance of the ProductionSystemConfig
prod = ProductionSystemConfig()
phaseTracker = ProductionSystemPhaseTracker(prod.monitoring_window, prod.evaluation_window)
# Print the configuration
print(prod)
# Print the phase tracker
print(phaseTracker)

