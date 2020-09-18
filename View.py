
def view_detection(nose_score, nose_x, nose_y, left_eye_y, right_eye_y, left_ear_score, right_ear_score,leftShoulder_x,right_eye_score, left_eye_score ):
	if (nose_score > 0.2) and (nose_y  < left_eye_y) and (nose_y > right_eye_y) and (left_eye_score > 0.2) and (right_eye_score > 0.2) and (nose_x < leftShoulder_x):
		return True
	else:
		return False
