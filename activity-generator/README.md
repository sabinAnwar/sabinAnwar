# GitHub Activity Generator

A Python script that generates a consistent, vibrant GitHub Contribution Graph for your account.

## Generated Activity Status
- **Repository**: [sabinAnwar/activity](https://github.com/sabinAnwar/activity) (Private)
- **Commits generated**: 1,709 commits across the past 365 days
- **Author**: `sabinAnwar` (`sabin.elanwar@iu-study.org`)

---

## ⚠️ Important GitHub Setting: Show Private Contributions

Because the generated repository is private (keeping your public project list clean and uncluttered), you need to make sure GitHub is configured to display private contributions on your public profile:

1. Go to your GitHub profile: [github.com/sabinAnwar](https://github.com/sabinAnwar)
2. Scroll down to the **Contribution Activity** section (just above your contribution graph calendar).
3. On the right side, click the dropdown **"Contribution settings"**.
4. Check the box for **"Private contributions"**.

> [!NOTE]
> GitHub may take 5 to 10 minutes to re-index and refresh your contribution graph tiles. Once processed, all past 365 days of green tiles will be displayed!

---

## How to Run Again in the Future

If you want to add more contributions or backfill another date range in the future:

```bash
python activity-generator/contribute.py -r https://github.com/sabinAnwar/activity.git -db 365 -fr 80 -mc 10
```

### Options & Flags:
| Flag | Description | Default |
|------|-------------|---------|
| `-r`, `--repository` | Link to GitHub remote repository (`https://github.com/user/repo.git`) | None |
| `-db`, `--days_before` | Number of days before today to generate commits for | `365` |
| `-da`, `--days_after` | Number of days after today to generate commits for | `0` |
| `-fr`, `--frequency` | Percentage (0-100) of days to commit on | `80` |
| `-mc`, `--max_commits` | Maximum number of commits per active day (1-20) | `10` |
| `-nw`, `--no_weekends` | Skip committing on Saturday and Sunday | `False` |
| `-un`, `--user_name` | Override Git `user.name` | System git config |
| `-ue`, `--user_email` | Override Git `user.email` (must match your GitHub email) | System git config |
