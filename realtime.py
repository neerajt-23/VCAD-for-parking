
def postProcess(outputs, img):
    global detected_classNames
    height, width = img.shape[:2]
    boxes = []
    classIds = []
    confidence_scores = []
    detection = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if classId in required_class_index and confidence > confThreshold:
                w, h = int(det[2] * width), int(det[3] * height)
                x, y = int((det[0] * width) - w / 2), int((det[1] * height) - h / 2)
                boxes.append([x, y, w, h])
                classIds.append(classId)
                confidence_scores.append(float(confidence))

    # Apply Non-Max Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidence_scores, confThreshold, nmsThreshold)
    indices = np.array(indices)  # Convert indices to a NumPy array
    for i in indices.flatten():
        x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]

        color = [int(c) for c in colors[classIds[i]]]
        name = classNames[classIds[i]]
        detected_classNames.append(name)
        # Draw classname and confidence score
        cv2.putText(img, f'{name.upper()} {int(confidence_scores[i]*100)}%',
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, font_size, color, font_thickness)

        # Draw bounding rectangle
        cv2.rectangle(img, (x, y), (x + w, y + h), color, font_thickness)
        detection.append([x, y, w, h, required_class_index.index(classIds[i])])

    # Update the tracker for each object
    boxes_ids = tracker.update(detection)
    for box_id in boxes_ids:
        count_vehicle(box_id, img)


def realTime():
    global total_count
    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
        ih, iw, channels = img.shape

        blob = cv2.dnn.blobFromImage(img, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)

        # Set the input of the network
        net.setInput(blob)
        outputNames = net.getUnconnectedOutLayersNames()

        # Feed data to the network
        outputs = net.forward(outputNames)

        # Find the objects from the network output
        postProcess(outputs, img)

        # Draw the crossing lines
        cv2.line(img, (0, middle_line_position), (iw, middle_line_position), (255, 0, 255), 2)
        cv2.line(img, (0, up_line_position), (iw, up_line_position), (0, 0, 255), 2)
        cv2.line(img, (0, down_line_position), (iw, down_line_position), (0, 0, 255), 2)

        # Draw counting texts in the frame
        cv2.putText(img, "Up", (110, 20), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(img, "Down", (160, 20), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(img, f"Car:        {up_list[0]}     {down_list[0]}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    font_size, font_color, font_thickness)
        cv2.putText(img, f"Motorbike:  {up_list[1]}     {down_list[1]}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX,
                    font_size, font_color, font_thickness)
        cv2.putText(img, f"Bus:        {up_list[2]}     {down_list[2]}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                    font_size, font_color, font_thickness)
        cv2.putText(img, f"Truck:      {up_list[3]}     {down_list[3]}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    font_size, font_color, font_thickness)

        # Display the total count of vehicles
        total_count = sum(down_list)
        cv2.putText(img, f"Total Count: {total_count}", (20, 140), cv2.FONT_HERSHEY_SIMPLEX,
                    font_size, font_color, font_thickness)

        # Show the message "Limit reached" if the total count of vehicles in the down section is more than 5
        if total_count > 5:
            cv2.putText(img, "Limit reached", (20, 160), cv2.FONT_HERSHEY_SIMPLEX,
                        font_size, (0, 0, 255), font_thickness)

        # Show the frames
        Sh = cv2.imshow('Output', img)

        if cv2.waitKey(1) == 27:
            break

    # Decrement total vehicle count by one if up_count is incremented
    if total_count > 0:
        total_count -= 1

    # Write the vehicle counting information in a file and save it
    with open("data.csv", 'w') as f1:
        cwriter = csv.writer(f1)
        cwriter.writerow(['Direction', 'car', 'motorbike', 'bus', 'truck'])
        up_list.insert(0, "Up")
        down_list.insert(0, "Down")
        cwriter.writerow(up_list)
        cwriter.writerow(down_list)
    f1.close()
    print("Data saved at 'data.csv'")

    # Finally release the capture object and destroy all active windows
    cap.release()
    cv2.destroyAllWindows()


# Call the realTime function to start the vehicle detection and counting
realTime()
