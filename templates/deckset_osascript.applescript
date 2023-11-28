-- Credit to https://github.com/deckset/deckset-scripts/blob/master/markdown-to-pdf/markdown-to-pdf.sh
on run argv
    set md_file to "{{markdown_abspath}}"
    set md_file to POSIX file md_file
    set out_file to "{{pdf_abspath}}"
    set out_file to POSIX file out_file
    tell application "Deckset"
        activate
        open file md_file
        tell document 1
            activate
            export to out_file printAllSteps {{print_all_steps}} includePresenterNotes {{include_presenter_notes}}
        end tell
    end tell
end run
