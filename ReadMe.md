# CorBot API

## How to add modules

1. One can place functions into modules as one likes as far as every function that is intended to be used through this API is imported to ```app.controller.dispatcher``` module and registered in a map called ```MAP``` that is situated at the bottom of that module.
1. If one's function has to use session or metadata, they have to be imported from module called ```app```.
1. Only modification to functions are:
    1. Replace all arguments with only one dict called ```data``` for now.
    1. Retrieve all needed arguments in the function from this ```data``` dict.

## Exceptions

1. In case some part of the program raising and exception one will get a json with ```error``` filed with a message.

## Example of creating request:
1. Go to corbot_api and send test request.

    1. In `Reg number` field add reg number.
    1. In `Subject` enter name of sevice.
    1. In `Body` field add data you need to send.

    ![alt text](read_me_images/weather.png)

