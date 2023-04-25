from time import sleep
import Stability.stab_test as test
import Stability.calculator as calc

# sleep(3)
# print (
#     test.run(test.Location.Javelin)
# )

# print(
#     calc.calc(
#         (
#             ((574, 753), (2023, 737)),
#             ((573, 517), (2028, 491))
#         )
#     )
# )

sleep(3)
print (
    calc.calc(test.run(test.Location.Javelin))
)