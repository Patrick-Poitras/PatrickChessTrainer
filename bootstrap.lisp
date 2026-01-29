(quicklisp:quickload :cl-raylib)
(use-package :cl-raylib)

(defstruct (chess-set/single-color (:conc-name p-))
  (king)
  (queen)
  (rook)
  (bishop)
  (knight)
  (pawn))

(defstruct chess-set
  (white-pieces)
  (black-pieces))

(defvar *chess-set* nil)

(defun load-chess-set ()
  (setf *chess-set* 
        (let ((white-pieces
                (make-chess-set/single-color
                 :king (load-texture-from-image (load-image "pieces/wK.png"))
                 :queen (load-texture-from-image (load-image "pieces/wQ.png"))
                 :rook (load-texture-from-image (load-image "pieces/wR.png"))
                 :bishop (load-texture-from-image (load-image "pieces/wB.png"))
                 :knight (load-texture-from-image (load-image "pieces/wN.png"))
                 :pawn (load-texture-from-image (load-image "pieces/wP.png"))))
              (black-pieces
                (make-chess-set/single-color
                 :king (load-texture-from-image (load-image "pieces/bK.png"))
                 :queen (load-texture-from-image (load-image "pieces/bQ.png"))
                 :rook (load-texture-from-image (load-image "pieces/bR.png"))
                 :bishop (load-texture-from-image (load-image "pieces/bB.png"))
                 :knight (load-texture-from-image (load-image "pieces/bN.png"))
                 :pawn (load-texture-from-image (load-image "pieces/bP.png")))))
          (make-chess-set :white-pieces white-pieces
                          :black-pieces black-pieces))))

(defun get-piece-image (color piece-access-func)
  (when (null *chess-set*) (load-chess-set))
  (funcall piece-access-func (ecase color
                               (:white (chess-set-white-pieces *chess-set*))
                               (:black (chess-set-black-pieces *chess-set*)))))

(defun draw-piece (color piece pos-x pos-y &key (scale 0.25f0 ))
  (draw-texture-ex (get-piece-image color piece) (3d-vectors:vec pos-x pos-y) 0f0 scale :red))

(defun initialize ()
  (init-window 400 400 "hello!")
  (load-chess-set)
  (set-target-fps 100))

(defun main-loop ()
  (loop :while (not (window-should-close))
          :do (progn (begin-drawing)
                     (clear-background :white)
                     (draw-piece :white 'p-rook 0 100)
                     (draw-text "testing" 50 50 20 :black)
                     (draw-fps 0 0)
                     (end-drawing))))

(defun terminate ()
  (close-window))

(defun run ()
  (initialize)
  (main-loop)
  (terminate))

(run)
