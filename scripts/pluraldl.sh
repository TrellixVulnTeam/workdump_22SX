user=$1
password=$2
course_name=$3
youtube-dl \
--verbose \
--username "${user}" \
--password "${password}" \
--sleep-interval 30 \
-o "${course_name}/%(playlist_index)s - %(title)s.%(ext)s" \
"https://app.pluralsight.com/library/courses/${course_name}"