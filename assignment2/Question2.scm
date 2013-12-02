#! /usr/bin/env racket

#lang scheme
;;; Question 2a
(define (someFunction num)
	(or (even? num) (= (remainder num 3) 0))
)

(someFunction 2)
(someFunction 3)
(someFunction 4)
(someFunction 5)


;;; Question 3
(define (remove_even lst)
	(cond 
	[(empty? lst) lst]
	[(even? (first lst)) (remove_even (rest lst))]
	[else (cons (first lst) (remove_even (rest lst)))]
	)
)

(remove_even (list 1 2 3 4 5 6 7 8 9 ))

;;;Question 4
(define (word lis)
  (if (null? lis)
      '()
      (append (word (cdr lis))
              (list (car lis)))))

(define (my_reverse str)
	(list->string (word (string->list str)))
)

(my_reverse "Apple")

;;;Question 5
;;;Use Lambda

(define (adder x)
	(lambda (a) (+ a x))
)

((adder 10) 9)
((adder 1) 8)
((adder 12) 8)
((adder 2) 8)
