import numpy as np

from utils.predictor import predict_profit


def optimize_channel_mix(base_input):

    best_profit = -999999999

    best_mix = None

    for ue in np.arange(0.1, 0.7, 0.1):

        for sd in np.arange(0.1, 0.7, 0.1):

            dd = 1 - (ue + sd)

            if dd <= 0:
                continue

            test = base_input.copy()

            test["UE_share"] = ue
            test["SD_share"] = sd
            test["DD_share"] = dd

            profit = predict_profit(test)

            if profit > best_profit:

                best_profit = profit

                best_mix = {

                    "UberEats": round(ue,2),
                    "SelfDelivery": round(sd,2),
                    "DoorDash": round(dd,2)
                }

    return best_mix, best_profit