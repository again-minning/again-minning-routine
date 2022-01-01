from enum import Enum, unique


@unique
class DeployState(Enum):
    LOCAL = 'local'
    STAGING = 'staging'
    PRODUCTION = 'production'
