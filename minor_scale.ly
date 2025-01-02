\version "2.22.0"  % Specify the LilyPond version


\paper {
  top-margin = 1.5\cm
  bottom-margin = 1.5\cm
  left-margin = 2\cm
  right-margin = 2\cm
  indent = 0
  line-width = 16\cm  % Adjust line width as needed
}

\score {

  \header {
    title = "Minor Scale in C"
    composer = "Traditional"
  }
  
  \new Staff {
    \relative c' {
      \key c \minor
      \time 4/4

      c4 d4 d#4 f4 g4 g#4 a#4 c4 d4 d#4 f4 g4 g#4 a#4 c4 a#4 g#4 g4 f4 d#4 d4 c4 a#4 g#4 g4 f4 d#4 d4 c4
    }
  }

  \layout {
    indent = 0  % Remove indentation to center the music
    ragged-right = ##t  % Allow ragged right margins
  }
  \midi { }
}

