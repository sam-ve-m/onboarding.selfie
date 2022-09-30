                                                                                                                                 #!/bin/bash
fission spec init
fission env create --spec --name selfie-env --image nexus.sigame.com.br/fission-async:0.1.7 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name selfie-fn --env selfie-env --src "./func/*" --entrypoint main.selfie --executortype newdeploy --maxscale 1
fission route create --spec --name selfie-rt --method POST --url /onboarding/post_selfie --function selfie-fn
