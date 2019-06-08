#!/usr/bin/env bash
#  Bash helper functions to put colors on your scripts
#
#  Usage example:
#  vargreen=$(echogreen "Grass is green")
#  echo "Coming next: $vargreen"
#

__RAINBOWPALETTE="1"

function __colortext()
{
  echo -e " \e[$__RAINBOWPALETTE;$2m$1\e[0m"
}

 
function echogreen() 
{
  echo $(__colortext "$1" "32")
}

function echored() 
{
  echo $(__colortext "$1" "31")
}

function echoblue() 
{
  echo $(__colortext "$1" "34")
}

function echopurple() 
{
  echo $(__colortext "$1" "35")
}

function echoyellow() 
{
  echo $(__colortext "$1" "33")
}

function echocyan() 
{
  echo $(__colortext "$1" "36")
}

# Bold Colors
# Usage: echo -e "${Blue}blue ${Red}red etc...."
#

RCol='\e[0m'
Black='\e[1;30m';
Red='\e[1;31m';
Green='\e[1;32m';
Grey='\e[1;32m';
Yellow='\e[1;33m';
Blue='\e[1;34m';
Purple='\e[1;35m';
Cyan='\e[1;36m';
White='\e[1;37m';