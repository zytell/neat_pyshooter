
class FrameCounter:
    __instance = None
    @staticmethod
    def get_instance():
        if FrameCounter.__instance is None:
            FrameCounter()
        return FrameCounter.__instance

    def __init__(self):
        self.frames = 0
        if FrameCounter.__instance is not None:
            raise Exception('This class is a singleton')
        FrameCounter.__instance = self

    @staticmethod
    def add_frame():
        if FrameCounter.__instance is None:
            raise Exception('Class needs to be initialised first.')
        FrameCounter.__instance.frames += 1

    @staticmethod
    def get_frames():
        if FrameCounter.__instance is None:
            raise Exception('Class needs to be initialised first.')
        return FrameCounter.__instance.frames

    @staticmethod
    def reset_frames():
        if FrameCounter.__instance is None:
            raise Exception('Class needs to be initialised first.')
        FrameCounter.__instance.frames = 0


def main():
    # f1 = FrameCounter.get_instance()
    # f2 = FrameCounter.get_instance()
    #
    # print(f1.frames, f2.frames)
    # f1.add_frame()
    # print(f1.frames, f2.frames)
    FrameCounter()
    FrameCounter.add_frame()
    print(FrameCounter.get_frames())


if __name__ == '__main__':
    main()
