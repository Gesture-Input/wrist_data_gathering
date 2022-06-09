from Modules import wristHandler

handler = wristHandler.WristHandler("rpf511",[4],['/dev/ttyACM0'],[9600])
handler.run_console()