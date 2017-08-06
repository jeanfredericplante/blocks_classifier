source ~/git-completion.bash
source .ec2rc
# Docker Alias
alias dpa="docker ps -a"
alias dks="docker start"
alias dka="docker attach"
alias dl="docker ps -l -q"
alias dksl="docker start `dl`"
alias dkal="docker attach `dl`"
dktm() { docker exec -it "$1" bash ;}

# Git alias
alias gcm='git commit -m'
alias gcam='git commit -am'
alias gpr='git pull --rebase'
