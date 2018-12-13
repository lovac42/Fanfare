# Fanfare
AnkiAddon: Gamification, feedback, and reinforcement

Anki Addon Link: https://ankiweb.net/shared/info/2073603704  
Themes Folder: https://www.dropbox.com/sh/kkiyc9gtcyn11om/AAAh0y4t4HIy2Z53HR5vRjrza


## About:
In the current Anki setup, we have kung fu cats for rewards and wiener dogs popping up in the middle of a review session. There's also a guy making fart noises intermittently. Not sure what that last one was about...but it's very distracting: cats-dogs-fart, cats-dogs-fart. This addon replaces the previous attempts with a unified theme.

<b>NOTE:</b> If you have other gamification addons, please disable them first as they might conflict with this one. Especially <a href="https://ankiweb.net/shared/info/1627107763">Kitten Rewards</a> and <a href="https://ankiweb.net/shared/info/1749604199">Visual Feedback for Review</a>, the predecessors of this addon.


## Themes:
Four sample themes are currently available at  
https://www.dropbox.com/sh/kkiyc9gtcyn11om/AAAh0y4t4HIy2Z53HR5vRjrza  
You need to download and unzip the files to "fanfare/user_files".

- Silhouette: the default theme included with the Anki addon.  
- YesNo: Simply displays yes and no feedbacks.  
- Trout_Slap: Quick flashes of trouts.  
- Bruce_Lee: Sound, images, and teachings of Master Bruce Lee.  

These themes will become stale when overused. But hopefully, as designers get interested in this, more themes will become available.  



## Audio:
This addon uses an audio API for playing soundFX which may not be compatible with all devices. It has been tested on Windows only. If you do not hear any sounds, edit the config with the addon manager and set "use_mplayer_for_audio" to true. Doing so will increase the lag time but should be portable across all devices.  

The volume can be change using the volume mixer of your OS.  


## Config:
You can use the addon manager to toggle certain features on/off. Anki 2.0 will require the <a href="https://ankiweb.net/shared/info/2058082580">backported addon manager</a> to change config settings.


## API USED:
playsound: https://pypi.org/project/playsound/#files



# FAQ:

### Why not randomize feedbacks?
Rewards should be randomized, feedbacks should not because it is already earned, something expected. Think of it as payday. How would you like it if your boss randomizes your pay date? Randomizing feedback frequency induces stress into your study sessions. Rewards on the other hand are like Xmas bonuses, they should be randomized. Remember, our primary goal here is to learn, gaming elements are added only to aid in learning. Just because an idea is fun for gaming isn't always a good idea for learning.

### Why insert FX between cards?
Anki records the timing of each review; how long it took before the "Show Answer" button was pressed. This information is reflected in your review logs and stats. Inserting FX between cards is the only way to eliminate any discrepancies in timing. Did you get distracted? Were your eyes wondering around looking at kittens or wiener dogs instead of the topic question? Except for day dreaming, it ensures that five seconds is actually five seconds of review time, no random pop ups. Accurate revLog is vital for future projects involving generating matrixes from Anki's review logs.

### Why the time gap?
What's wrong with that? Supermemo forces the user to press the spacebar after each review. This sort pause ensures that users are digesting their studying material one piece at a time. Jumping from card to card without any digestions or reflection will lead to unstable memory and lapses. And these lapses will mount up causing large amounts of reviews. So what's wrong with chewing your food before taking another bite?

The pause between cards are theme dependent. It is up to the theme designer to decide how much time to pause, how long they should flash their artwork at the user. If you don't like long pauses, you may change the duration for each theme in the theme setting file.


