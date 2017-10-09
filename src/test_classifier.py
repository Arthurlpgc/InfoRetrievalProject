from classifier import predict

with open("good_sample_page.html") as myfile:
    prediction = predict.check_if_is_coding_question(myfile)
    print("This page is " + prediction)

with open("bad_sample_page.html") as myfile:
    prediction = predict.check_if_is_coding_question(myfile)
    print("This page is " + prediction)
