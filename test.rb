require 'open3'

id = 111111112
filePath = "./speaker_verification/tests/input"

enrollment = "python -m speaker_verification enroll --id #{id} --audio-path #{filePath}/enrollment.flac"
stdout, stderr, status = Open3.capture3(enrollment)
print "ruby enrollment complete... \n"

validate = "python -m speaker_verification validate --id #{id} --audio-path #{filePath}/validation.flac"
stdout, stderr, status = Open3.capture3(validate)
print "ruby validate stdout recieves: #{stdout} \n"
