import System.IO

parse :: String -> [[Int]]
parse = map (map (read::(String -> Int)) . words) . lines

sign x
    | x > 0 = 1
    | x < 0 = -1
    | x == 0 = 0

allsame [x] = (True, 0)
allsame (x:xs) =
    let k = x - head xs in
    let g = abs k in
    let w = allsame xs in ((sign k == snd w || (length xs == 1)) && fst w && g >= 1 && g <= 3, sign k)

dropAt n xs = take n xs ++ drop (n + 1) xs

safe = fst . allsame

actSafe xs = fromEnum $ safe xs || any (\ n -> safe $ dropAt n xs) [0..(length xs - 1)]

main :: IO ()
main = do
    h <- openFile "inp.txt" ReadMode
    c <- hGetContents h
    print $ sum $ map actSafe $ parse c