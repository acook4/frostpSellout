# frostpSellout

These programs were created for a giveaway hosted by FrostPrime_. 
To win $100 (increasing by $100 each week), people can redeem a channel points reward on Twitch to guess a number between 1 and 1 million. 
Guessing the correct number means that you will win.
People are limited to 1000 guesses a week and were allowed to use bots.

This "bot" has two programs;
one that collects numbers that have and haven't been guessed to determine a little of guessable numbers, 
and one that uses desktop automation to redeem the Twitch channel points reward.
The list of guessable numbers is determined using API from https://www.twentypoo.com, a site that gathers every guess made.

One detail of the number collecting program is how it determines which numbers should be guessed. 
One week, I heard Frost mention that the closest someone had gotten was within 30 of the real answer. 
So, this program looks for unguessed numbers within a configurable amount of already guessed numbers.
