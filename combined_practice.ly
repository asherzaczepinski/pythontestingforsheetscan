
\version "2.24.4"  % Force LilyPond to treat code with this version

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
    system-count = #0
    line-width = 16\cm  % Adjust as needed
}


\markup \column {
  \center-column {
    \bold "F# Major Scale"
  }
}

\score {
  \new Staff {
    % Force all accidentals to show (for any sharp or flat).
    \override Accidental #'force-accidental = ##t

    % Explicitly hide the time signature
    \set Score.timeSignatureVisibility = ##f

    \relative fis' {
      fis4 gis4 ais4 b4 cis4 dis4 f4 fis4 gis4 ais4 b4 cis4 dis4 f4 fis4 f4 dis4 cis4 b4 ais4 gis4 fis4 f4 dis4 cis4 b4 ais4 gis4 fis4
    }
  }
  \layout {
    indent = 0
    ragged-right = ##t
  }
  \midi { }
}


\markup \column {
  \center-column {
    \bold "D# Minor Scale"
  }
}

\score {
  \new Staff {
    % Force all accidentals to show (for any sharp or flat).
    \override Accidental #'force-accidental = ##t

    % Explicitly hide the time signature
    \set Score.timeSignatureVisibility = ##f

    \relative dis' {
      dis4 f4 fis4 gis4 ais4 b4 cis4 dis4 f4 fis4 gis4 ais4 b4 cis4 dis4 cis4 b4 ais4 gis4 fis4 f4 dis4 cis4 b4 ais4 gis4 fis4 f4 dis4
    }
  }
  \layout {
    indent = 0
    ragged-right = ##t
  }
  \midi { }
}

