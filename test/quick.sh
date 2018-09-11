#!/bin/bash

# just really quick bash tests with the great tool httpie...
# brew install httpie

http http://localhost:8100/api/me

http POST http://localhost:8100/api/login email="howdy@example.com" password="moomoo"

