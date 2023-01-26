import os
import openai
# INSERT YOUR PRIVATE API KEY HERE
PRIVATE_API_KEY = "WRITE_YOUR_PRIVATE_API_KEY"

class Request:
    def __init__(self):
        self.line_repetition = 0.5
        self.randomness = 0.5
        self.max_line = 6
        self.min_line = 3
    
    # in charge of updating the hyperparameters
    def change_preferences(self, line_repetition, randomness, max_line, min_line):
        self.line_repetition = line_repetition
        self.randomness = randomness
        self.max_line = max_line
        self.min_line = min_line
    
    # in charge of aggregating a prompt, give in to the GPT-3 to create a respond. return the response and the request
    def get_response(self, creation_type, size, genre, subject, context):
        request = "write a {} in the {} genre about a {} in the context of {} with only {} lines, where the max length of a line is {} words and the minimum length is {} words".format(
            creation_type, genre,  subject, context, size, self.max_line, self.min_line)
        creation = ["song", "limerick", "poem"]
        for type in creation:
            if type in subject:
                request = request.replace(type, "")
        print(request)
        openai.api_key = PRIVATE_API_KEY
        try:
            completion = openai.Completion.create(model="text-davinci-003",
                                                  prompt=request,
                                                  max_tokens=4000,
                                                  temperature=0.2,
                                                  presence_penalty=self.randomness,
                                                  frequency_penalty=self.line_repetition, )
            response = completion.choices[0].text
            response = self.check_genre(response, genre)
            response = self.check_length(response, size, subject, context,genre)
            response = response.split("\n")[2:]
            response = "\n".join(response)

        except openai.error.ServiceUnavailableError or openai.error.RateLimitError:
            response = "Unfortunately your parameters weren't loaded properly. Try again"
        return response, request

    # checks if the generated song's genre is correct. If not, a new response is created. returns this response
    def check_genre(self, response, genre):
        openai.api_key = PRIVATE_API_KEY
        request = "what is the genre of the song you created? Write only the genre without a dot"
        print(request)
        completion = openai.Completion.create(model="text-davinci-003", prompt=request, max_tokens=4000,
                                              temperature=0.2,
                                              presence_penalty=self.randomness,
                                              frequency_penalty=self.line_repetition, )
        response_of_genre = completion.choices[0].text
        print(response_of_genre)
        if genre not in response_of_genre:
            request = "redo the song to be from the {} genre while keeping the subject " \
                      "and the max length of a line is {} words and the minimum length is {} words".format(genre, self.max_line, self.min_line)
            completion = openai.Completion.create(model="text-davinci-003", prompt=request, max_tokens=4000,
                                                  temperature=0.2,
                                                  presence_penalty=self.randomness,
                                                  frequency_penalty=self.line_repetition, )
            response = completion.choices[0].text
        return response

    # checks if the generated song's length is correct. If not, a new response is created. returns this response
    def check_length(self, response, size, subject, context,genre):
        if size != len(response):
            request = "redo the song to have exactly {} lines while keeping the subject {} in the context of {}, genre {}" \
                      "and the max length of a line is {} words and the minimum length is {} words".format(size, subject, context,genre,self.max_line, self.min_line)
            completion = openai.Completion.create(model="text-davinci-003", prompt=request, max_tokens=4000,
                                                  temperature=0.2,
                                                  presence_penalty=self.randomness,
                                                  frequency_penalty=self.line_repetition, )
            response = completion.choices[0].text
        return response


# for local testing
if __name__ == '__main__':
    request = Request()
    print(request.get_response("song", "20", "pop", "Ofra", "nature"))
