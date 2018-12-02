# Fanfare
AnkiAddon: Gamification, feedback, and reinforcement

https://ankiweb.net/shared/info/2073603704


## About:
In the current Anki setup, we have kung fu cats for rewards and wiener dogs popping up in the middle of a review session. There's also a guy making fart noises intermittently. Not sure what that last one was about...but it's very distracting: cats-dogs-fart, cats-dogs-fart. This addon replaces the previous attempts with a unified theme. Two sample themes are currently included: Silhouette and Bruce_Lee. The Bruce_Lee theme will work well with <a href="https://ankiweb.net/shared/info/715575551">Life Drain</a> to induce a small amount of excitement into the reviews. Of course, they become stale when overused. But hopefully, as designers get interested in this, more themes will become available.  

<b>NOTE:</b> If you have other gamification addons, please disable them first as they might conflict with this one. Especially <a href="https://ankiweb.net/shared/info/1627107763">Kitten Rewards</a> and <a href="https://ankiweb.net/shared/info/1749604199">Visual Feedback for Review</a>, the predecessors of this addon.


## Audio:
This addon uses an audio API for playing soundFX which may not be compatible with all devices. It has been tested on Windows only. If you do not hear any sounds, edit the config with the addon manager and set "use_mplayer_for_audio" to true. Doing so will increase the lag time but should be portable across all devices.  

The volume can be change using the volume mixer of your OS.  


## Config:
You can use the addon manager to toggle certain features on/off. Anki 2.0 will require the <a href="https://ankiweb.net/shared/info/2058082580">backported addon manager</a> to change config settings.


## API USED:
playsound: https://pypi.org/project/playsound/#files

