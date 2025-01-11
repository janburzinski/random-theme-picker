# Themes Loader

# miau

The Themes Loader is supposed to save a .json file with a lot of the themes from jetbrains and
vs code

# why

this is to not overload their api / rate limit ourselves and just load the data from storage
this also probably makes things a lot faster and easier since i can just load from a json file on
each new theme I want to get

# how to get preview img from vs code theme

as microsoft doesn't return a preview image link (like jetbrains), we try to get the preview image from the README.md of the github repo from the theme.
as microsoft very easily ratelimits you (10req./s; ~20s), we have to always keep track of the X-RateLimit-Remain.
