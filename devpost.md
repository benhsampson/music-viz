## Inspiration

Our group, being rave and concert goers, was initially inspired by the laser and light shows delivered at such events. It seemed quite apparent anecdotally, and in the widespread adoption of accompanying visual spectacles, that an auditory experience can be synergistically enhanced by engaging other human senses, especially sight.

As such we thought about the health implications of such a technology. It is widely understood and researched that music has a role in pain management (1), and mental wellbeing (2). These findings are ubiquitous within (3)  and without (4) healthcare settings, and non-discriminating by age (5, 6). 

One area of implementation is the use in paediatric functional constipation which is a common ailment with significant impact on the affected child and their parents (7). An aspect of this disease we hope to improve through MusicViz is to reduce the anxiety and pain associated with the toilet for children (8) by enhancing music therapy with accompanying visual stimuli. 

## What it does

Existing audio visualising technologies seem to only decompose music and sounds into a composition of frequencies and visualise audio in a frequency-amplitude domain. What we hope to achieve with MusicViz is to gain a deeper insight into music through Neuro-Linguistic Programming (NLP) and music analysis to extract its characteristics.

MusicViz would be attempting to extract the technical components of a piece such as its keys and key changes, tempo and rhythm, chords, consonances and dissonances. Combined with analysis of melody, lyrics to provide more insight into more nuanced and complex concepts such as the themes, mood, tension and release of the piece. Then based on its analysis, produce a synchronised visual representation of the piece in the form of an LED light show. 

## How we built it

In order to build towards a minimum viable product (MVP), our team deconstructed the concept into its core components. The cores identified were music analysis, visualiser logic, and hardware.

A large part of the project was research conducted into music analysis and music composition to isolate the most relevant components. Following which was working out how to extract such information from a piece of music.

The Librosa library proved invaluable in decomposing a track to enable deeper analysis. Through signal processing and the development of computer logic we were able extract the relevant information in a track.

We also developed logic to transform the audio input into a visual representation through further signal processing. This also required us to develop understanding into colour theory and associating this with music composition and emotions to output a coherent experience. 

Due to time constraints, a decision was made to simplify the visualisation to an 8 x 8 LED array to demonstrate MusicVis. A python simulation was constructed using the matplotlib library to help visualise implementations of the our developed logic. 

Lastly was the construction of the LED matrix required sourcing various components to physically demonstrate our product.

## Challenges we ran into

Major challenges the team encountered were largely resultant from our lack of experience in different domains but we were motivated to build our breadth and learn new skills. 

Only one member had experience with music but they have not had much experience with the intricacies of music theory. 

Librosa, though powerful, was a library that was new to the team thus requiring time to build familiarity with its use.

Developing the logic took a lot of trial and error and deepening our understanding of signal processing - we expect further tweaking will be necessary to achieve better polish.

Using and programming LEDs was new to the team as well, necessitating learning of the hardware requirements to build the product.

## Accomplishments that we're proud of

Being able to construct both the software and hardware for a MVP within the timeframe of the UniHack was something our team is proud of.

We hope by further developing this product we might be able to help children with their constipation, as well as provide a product for general consumer use.

## What we learned

To summarise:

- Learning about music composition and music theory
- Learning to use the Librosa library
- Learning how to implement NLP
- Learning signal processing
- Learning colour theory 
- Learning how to program and build LED products

## What's next for MusicVis

Currently MusicVis does this by preprocessing a musical piece but the hope in the future is that it would be able to perform this as close to realtime as possible and extrapolate to more sophisticated lighting systems.

An additional function we would really like to develop would be the capabilities to integrate the user's live environment and mood to make appropriate musical choices on their behalf to enhance a user's experience.

## References
1. Garza-Villarreal, E. A., Pando, V., Vuust, P., & Parsons, C. (2017). Music-Induced Analgesia in Chronic Pain Conditions: A Systematic Review and Meta-Analysis. Pain physician, 20(7), 597–610.

1. Lu G, Jia R, Liang D, Yu J, Wu Z, Chen C. Effects of music therapy on anxiety: A meta-analysis of randomized controlled trials. Psychiatry Res. 2021;304:114137. doi:10.1016/j.psychres.2021.114137

1. Dallı ÖE, Yıldırım Y, Aykar FŞ, Kahveci F. The effect of music on delirium, pain, sedation and anxiety in patients receiving mechanical ventilation in the intensive care unit. Intensive Crit Care Nurs. 2023;75:103348. doi:10.1016/j.iccn.2022.103348

1. Terry PC, Karageorghis CI, Curran ML, Martin OV, Parsons-Smith RL. Effects of music in exercise and sport: A meta-analytic review. Psychol Bull. 2020;146(2):91-117. doi:10.1037/bul0000216

1. Ke X, Song W, Yang M, Li J, Liu W. Effectiveness of music therapy in children with autism spectrum disorder: A systematic review and meta-analysis. Front Psychiatry. 2022;13:905113. Published 2022 Oct 6. doi:10.3389/fpsyt.2022.905113

1. Gómez-Romero M, Jiménez-Palomares M, Rodríguez-Mansilla J, Flores-Nieto A, Garrido-Ardila EM, González López-Arza MV. Benefits of music therapy on behaviour disorders in subjects diagnosed with dementia: a systematic review. Beneficios de la musicoterapia en las alteraciones conductuales de la demencia. Revisión sistemática. Neurologia. 2017;32(4):253-263. doi:10.1016/j.nrl.2014.11.001

1. Vriesman MH, Rajindrajith S, Koppen IJN, et al. Quality of Life in Children with Functional Constipation: A Systematic Review and Meta-Analysis. J Pediatr. 2019;214:141-150. doi:10.1016/j.jpeds.2019.06.059

1. Kids Health Info : Constipation (no date) www.rch.org.au. Available at: https://www.rch.org.au/kidsinfo/fact_sheets/Constipation/.