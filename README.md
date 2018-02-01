# Humming Bird (featured @ SheHacks Boston 2018)

## Inspiration
According to WHO, more than 300 million people worldwide are affected with depression. At its worst, depression can lead to suicide and close to 800,000 people die due to suicide every year. Suicide is the second leading cause of death in 15-29-year-olds. Most of the time, people experiencing mental illness are unaware they have a mental illness until it has progressed too far.

## What it does
People often keep their thoughts to themselves; some keep a journal. Hummingbird listens to your thoughts and gives an analysis of what factors are affecting your mental state. It does more than simply identifying a persons usual mood fluctuations and short-lived emotional responses to challenges in everyday life. It gives a time series analysis of your positive and negative sentiments over longer span and gives a close summary of the entities playing a role in your daily life. It empowers a person to pinpoint the events and or person that are having a positive or negative influence in your life using AI. It makes people aware of their mental state so that they seek help before they are very deep down in depression.

### How we built it
Our team used language API from google cloud platform to list the entities and the positive or negative influence the entities are having on individuals. It also uses nltk hypernyms to group similar entities into a category. Thus indicating the largest source of an individuals worries. For instance, if a person is constantly thinking about their weight gain/loss, clothing, grooming etc it can be said that the person is very concerned about their appearance. If these thoughts have a negative sentiment score persistent over a long period of time and appears more frequently in the journal, it can be said that this entity/category have a negative influence in their lives.
