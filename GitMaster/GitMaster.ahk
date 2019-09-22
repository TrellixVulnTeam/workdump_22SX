; https://www.autohotkey.com/docs/KeyList.htm
#SingleInstance force
CoordMode, Mouse, Screen;

:*:;rg::
{
	Run "C:\Program Files\Git\usr\bin\bash.exe" -l
	Return
}

:*:;sl::
{
	cmd = subl "%clipboard%"
	Send, %cmd%
}

:*:;gsg::git status | grep -E{SPACE}
:*:;ga.::git add .
:*:;gau::git add -u
:*:;gca::git commit -a
:*:;gcb::git checkout{SPACE}
:*:;gcd::cd ~/git/coleman.ui/
:*:;gcf::git commit --fixup=HEAD
:*:;gcm::git commit -m ""{LEFT}
:*:;gcp::git cherry-pick{SPACE}
:*:;gdt::git tag -d{SPACE}
:*:;gfa::git fetch --all
:*:;gfph::git push -f
:*:;gfpl::git pull -f
:*:;gg::git grep -n --break --heading -E ""{LEFT}
:*:;glt::git ls-tree -r --name-only HEAD | grep -E ""{LEFT}
:*:;glg::git log --date=short --pretty=format:"%ad:%Cgreen%an:%Cred%h%d:%Creset%s"
:*:;gncp::git cherry-pick --no-commit{SPACE}
:*:;gph::git push{SPACE}
:*:;gpl::git pull{SPACE}
:*:;grb::git rebase origin/
:*:;gra::git rebase --abort
:*:;grc::git rebase --continue
:*:;grh::git reset --hard{SPACE}
:*:;gri::git rebase -i --autosquash HEAD~
:*:;gsri::git stash && git rebase -i --autosquash HEAD~ && git stash pop{LEFT 17}
:*:;grpl::git pull origin master --rebase
:*:;grs::git reset --soft{SPACE}
:*:;gst::git status
:*:;gtg::git tag{SPACE}
:*:;gxtg::git tag -d temp{SPACE};{SPACE}git tag temp
