import json
import openai
import os

openai.api_key = os.environ['api_key']

numberOfEssays = 60

response = openai.Completion.create(
  model="text-davinci-003",
  prompt=
  "Write an essay over 100 words on why you love Orville Redenbacher popcorn.\n",
  temperature=0.85,
  max_tokens=256,
  top_p=1,
  n=numberOfEssays,
  frequency_penalty=0,
  presence_penalty=0)

# Creates the library for all the essays "index": essay
data = {}

for i in range(numberOfEssays):
  data[str(response.choices[i].index)] = response.choices[i].text.strip()

# Review each essay ensure none are the same, and they are all atleast 100 words long
badEssayIndicies = []
for i in range(len(data)):
  wordCount = len(data[str(i)].split())
  if wordCount < 100:
    print("oh no, essay " + str(i) + " is less than 100 words.")
    badEssayIndicies.append(i)

  for compare in range(len(data)):
    if i != compare:
      if data[str(i)] == data[str(compare)]:
        badEssayIndicies.append(compare)

# Dumps essays with coresponding indecies in json file
essayFile = open("leif2AIEssays.json", "w")
json.dump(data, essayFile)
essayFile.close()

print(badEssayIndicies)
