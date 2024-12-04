import System.IO
import Data.List (sort)

isSep :: Char -> Bool
isSep '\n' = True
isSep ' ' = True
isSep c = False

wordss :: String -> [String]
wordss s = case dropWhile isSep s of
    "" -> []
    s' -> w : wordss s'' where (w, s'') = break isSep s'

main :: IO ()
main = do
    h <- openFile "inp.txt" ReadMode
    c <- hGetContents h
    let k = zip (map (read::(String -> Int)) (wordss c)) [1..]
    let (a, b) = ([ fst n | n <- k, odd $ snd n], [ fst n | n <- k, even $ snd n])
    let c = zipWith (curry (\ n -> abs (fst n - snd n))) (sort a) (sort b)
    print $ sum c