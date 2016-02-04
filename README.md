my-will
=======

My willbot implementation

DONE:
 * Emoticons
 * Generate a UUID
 * Hangman
 * Define
 * TFL status
 * Ascii me
 * YouTube

TODO:
 * Text FX:
  * Lorem ipsum
  * Hodor
 * Lists & searching (admin through web?):
  * Board Games
  * Lunch
 * Search internet sites:
  * Sporkle
  * Wiktionary
  * Wikipedia
  * XKCD
  * Dilbert
  * Nutscapes
 * Basic responders:
  * War games
  * Word of the day
  * Hello
  * Goodbye
 * Random:
  * In a specific room, set a random topic every 10 minutes from chatoms
  * Rage
  * Random rage
  * Random refusal to work
  * Willisms

TOIMPROVE:
 * Hangman
  * Make it look better
  * Persist over restart
  * Keep stats
   * Word length vs. guesses taken
   * Correct vs. incorrect guesses
   * Words that have been used (& their definitions)
   * Actual letter frequency vs. guessed letter frequency
   * Correct guesses per person vs. incorrect

TOFIX:
 * Respond to invitations

FAILED:
 * Restart
  * Will catches ALL exceptions. I tried monkey patching the listener to die but it seems to auto restart just that thread.
