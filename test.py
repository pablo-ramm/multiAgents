import numpy as np

pos_always_turn = {
    (13,15): lambda x: print("Always Turn Left - 9"),
    (18,12): lambda x: print("Always Turn Right - 11"),
    (18,15): lambda x: print("Always Turn Up - 12"),
    (19,20): lambda x: print("Always Turn Up - 16"),
    (20,19): lambda x: print("Always Turn Down - 20")
}

pos_could_turn = {
    (11,19): lambda x: print("Has a {} chance to turn Left - 4".format(np.random.rand())),
    (12,19): lambda x: print("Has a {} chance to turn Left - 6".format(np.random.rand())),
    (12,20): lambda x: print("Has a {} chance to turn Left - 7".format(np.random.rand())),
    (19,12): lambda x: print("Has a {} chance to turn Right - 14".format(np.random.rand())),
    (19,19): lambda x: print("Has a {} chance to turn Down - 15".format(np.random.rand())),
    (20,11): lambda x: print("Has a {} chance to turn Down - 18".format(np.random.rand())),
    (20,12): lambda x: print("Has a {} chance to turn Right - 19".format(np.random.rand()))
}

print(pos_could_turn[(11,19)](1))