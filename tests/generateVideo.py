from cv2 import imread
from cv2 import imshow
from cv2 import VideoWriter
from cv2 import waitKey
from cv2 import destroyAllWindows
from cv2 import VideoWriter_fourcc

frame = imread("tests/hello.png")
print (frame)
width, height, layer = frame.shape

out = VideoWriter("tests/out.avi", VideoWriter_fourcc(*'DIVX'), 15.0, (width, height))
for _ in range(1000):
    out.write(frame)

    imshow("Frame", frame)

    if waitKey(1) & 0xFF == ord("q"):
        break

out.release()