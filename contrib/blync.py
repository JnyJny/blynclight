#!/usr/bin/env python3

from blynclight import BlyncLight
import click
from time import sleep

@click.command()
@click.option('-l', '--light-id', default=0)
@click.option('-r', '--red', default=0)
@click.option('-b', '--blue', default=0)
@click.option('-g', '--green', default=0)
@click.option('--off/--on', default=True)
@click.option('--bright/--dim', default=False)
@click.option('--flash/--no-flash', default=False)
@click.option('-s', '--speed', default=0)
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('-d', '--duration', default=-1)
def cli(light_id, red, blue, green, off, bright, flash, speed, verbose, duration):
    '''
    '''
    light = BlyncLight.get_light(light_id)
    with light.updates_paused():
        light.red = red
        light.blue = blue
        light.green = green
        light.off = off
        light.dim = bright
        light.flash = flash
        light.speed = speed
        
    if verbose:
        print(light)
        
    while duration != 0:
        duration -= 1
        sleep(1)


#def main():
#
#    parser = ArgumentParser()
#    parser.add_argument("-l", "--light", type=int, default=-1)
#    parser.add_argument("-r", "--red", type=int, default=0)
#    parser.add_argument("-b", "--blue", type=int, default=0)
#    parser.add_argument("-g", "--green", type=int, default=0)
#    parser.add_argument("-o", "--on", action="store_true", default=False)
#    parser.add_argument("-d", "--dim", action="store_true", default=False)
#    parser.add_argument("-f", "--flash", action="store_true", default=False)
#    parser.add_argument("-s", "--speed", type=int, default=0)
#    parser.add_argument("-m", "--music", type=int, default=0)
#    parser.add_argument("-n", "--dryrun", action="store_true", default=False)
#    parser.add_argument("-p", "--play", action="store_true", default=False)
#    parser.add_argument("-R", "--repeat", action="store_true", default=False)
#    parser.add_argument("-M", "--mute", action="store_true", default=False)
#    parser.add_argument("-v", "--volume", type=int, default=0)
#    parser.add_argument("-V", "--verbose", action="store_true", default=False)
#    parser.add_argument("--list", action="store_true", default=False)
#
#    args = parser.parse_args()
#
#    if args.list:
#        for i, light in enumerate(BlyncLight.light_info()):
#            print(i, repr(light))
#        exit(0)
#
#    if args.light >= 0:
#        light = BlyncLight.available_lights()[args.light]
#    else:
#        light = BlyncLight.first_light()
#
#    light.immediate = False
#    light.red = args.red
#    light.blue = args.blue
#    light.green = args.green
#    light.on = args.on
#    light.dim = args.dim
#    light.flash = args.flash
#    light.speed = args.speed
#    light.music = args.music
#    light.play = args.play
#    light.repeat = args.repeat
#    light.mute = args.mute
#    light.volume = args.volume
#
#    if not args.dryrun:
#        light.update_device()
#
#    if args.verbose or args.dryrun:
#        print(light)


if __name__ == "__main__":
    cli()
