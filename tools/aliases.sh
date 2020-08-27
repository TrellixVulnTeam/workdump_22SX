# Usage: Append the file ~/.<shell>rc with the following command: source workdump/tools/aliases.sh

export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
cd ~/Repositories

alias ssh='cd ~ && ssh '
alias caf='/Applications/Caffeine.app/Contents/MacOS/Caffeine -u'
alias yt='youtube-dl --format "bestvideo[height<=1080]+bestaudio/best" --continue --sub-lang en --write-sub --write-auto-sub --no-check-certificate --verbose $(pbpaste) &'
alias gf='git fetch --all '
alias gl='git log --date=short --pretty=format:"%ad:%Cgreen%an:%Cred%h%d:%Creset%s" '
alias grh='git reset --hard '
alias gs='git status '
alias ga='git add . '
alias gcm='git commit -m '
alias gcf='git commit --fixup=HEAD '
alias gg='git grep -n --break --heading -E '
alias glg='git ls-tree -r --name-only HEAD | grep -E '
alias gri='git rebase -i --autosquash '

echo "Successfully loaded custom aliases."
