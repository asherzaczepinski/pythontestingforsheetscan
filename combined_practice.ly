\version "2.24.4"  % Specify the LilyPond version

\header {
  title = "Practice Scales"
  composer = "Traditional"
}

\paper {
  top-margin = 1.5\cm
  bottom-margin = 1.5\cm
  left-margin = 2\cm
  right-margin = 2\cm
  indent = 0
  system-count = #0  % Allow multiple systems
  line-width = 16\cm  % Adjust line width as needed
}

\markup \column {
  \center-column {
    \bold "Major Scale in A (Major)"
  }
}

\score {
  \new Staff {
    \relative a' {
      \key a \major
      \time 4/4

      a4 b4 cis4 d4 e4 fis4 gis4 a4 b4 cis4 d4 e4 fis4 gis4 a4 gis4 fis4 e4 d4 cis4 b4 a4 gis4 fis4 e4 d4 cis4 b4 a4
    }
  }

  \layout {
    indent = 0  % Remove indentation to center the music
    ragged-right = ##t  % Allow ragged right margins
  }
  \midi { }
}

\markup \column {
  \center-column {
    \bold "Minor Scale in F# (Minor)"
  }
}

\score {
  \new Staff {
    \relative f#' {
      \key f# \minor
      \time 4/4

      fis4 gis4 a4 b4 cis4 d4 e4 fis4 gis4 a4 b4 cis4 d4 e4 fis4 e4 d4 cis4 b4 a4 gis4 fis4 e4 d4 cis4 b4 a4 gis4 fis4
    }
  }

  \layout {
    indent = 0  % Remove indentation to center the music
    ragged-right = ##t  % Allow ragged right margins
  }
  \midi { }
}

