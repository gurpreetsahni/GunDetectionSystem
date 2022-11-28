import cv2
import numpy as np
import tempfile
#import winsound
import streamlit as st 
from twilio.rest import Client
import os


# My Twilio recovery Code :- 9zuJ6L0MS0I734uZX70N4S6-nLY3rgHvR6N2Adds
account_sid= 'AC783bccd15ef770c344a9ab74eaa68778'
auth_token ='fb3fc986dc276b76e41c307a0a97eedb'
client = Client(account_sid, auth_token)
net = cv2.dnn.readNet(r"./yolov3_training_2000.weights", r"./yolov3_testing.cfg")
classes = ["Weapon"]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# html Gun Dedection
html = '''
<div style="background-color:#9AC293;padding:13px;border-radius:20px">
<h1 style="color:black;text-align:center;"> Gun Detection For Security Surveillance </h1>
'''
st.markdown(html, unsafe_allow_html=True)
st.markdown('<h4 style="color:black;text-align:center;"> Dedect the Gun and save the life </h4>', unsafe_allow_html=True)
st.write("#")
uploaded_file = st.file_uploader("Choose a video for cheak")
if uploaded_file is not None:
	tfile = tempfile.NamedTemporaryFile(delete=False)
	tfile.write(uploaded_file.read())
	#st.video(tfile.name)
	cap = cv2.VideoCapture(tfile.name)
	
	def value(val):
	    #val = uploaded_file.get
	    #val = input("Enter file name or press enter to start webcam : \n")
	    if val == "":
	        val = 0
	    return val
		
	count=0
	gun=0
	final_img = st.empty()
	while True:
	    _, img = cap.read()
	    height, width, channels = img.shape
	    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
	    net.setInput(blob)
	    outs = net.forward(output_layers)
	    class_ids = []
	    confidences = []
	    boxes = []
	    for out in outs:
	        for detection in out:
	            scores = detection[5:]
	            class_id = np.argmax(scores)
	            confidence = scores[class_id]
	            if confidence > 0.5:
	                center_x = int(detection[0] * width)
	                center_y = int(detection[1] * height)
	                w = int(detection[2] * width)
	                h = int(detection[3] * height)
	                x = int(center_x - w / 2)
	                y = int(center_y - h / 2)
	                boxes.append([x, y, w, h])
	                confidences.append(float(confidence))
	                class_ids.append(class_id)
	    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
	    font = cv2.FONT_HERSHEY_PLAIN
	    print(indexes)
	    if indexes == 0:
	        duration = 2 #second
	        frequency = 500 #hz
	        gun+=1
	        print("weapon detected in frame")
	        # winsound.Beep(frequency,duration)
	        
	        os.system('play -nq -t alsa synth {} sine {}'.format(duration, frequency))
	        count+=1
	        if count==1:
	        #st.error("Alert, Weapon dedected in the video")
	            call = client.calls.create(
	                            url='http://demo.twilio.com/docs/voice.xml',
	                            from_='+16194859230',
	                            to='[+][91][8700549261]'
	                        )
	
	            print(call.sid)      
	    else:
	        print("weapon not detected in a frame")
	        #cv2.putText(img,"No Weapon", (50,50), font, 3,(255,0,255), 3)
	    for i in range(len(boxes)):
	        if i in indexes:
	            x, y, w, h = boxes[i] 
	            label = str(classes[class_ids[i]])
	            color = colors[class_ids[i]]
	            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
	            cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
	    #cv2.imshow("Image", img)
	   # cv2.namedWindow("output", cv2.WINDOW_NORMAL)
	   # cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
	   # cv2.imshow("Image", ing)
	    #st.image(img)
	    final_img.image(img)
	    key = cv2.waitKey(1)
	    if key == 27:
	        break
	cap.release()
	cv2.destroyAllWindows()	
	if gun == 0:
		st.error(" No Gun found in video ")
	else:
     	#st.image(img)
		st.success(" Gun dedected in video ")
     	
