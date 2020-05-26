import System.Environment (getArgs)
import Data.List
import Data.Time.Clock

dot :: [Int] -> [Int] -> Int
dot x y = sum $ zipWith (*) x y

matrixproduct :: [[Int]] -> [[Int]] -> [[Int]]
matrixproduct m1 m2 = [[dot x y | y<-transpose m2] | x<-m1 ]

main :: IO()
main = do
    args <- getArgs
    let n = read $ head args ::Int
    let a=[[i*n+j | j<-[0..n-1]] | i<-[0..n-1]]
    let b=[[j*n+i | j<-[0..n-1]] | i<-[0..n-1]]
    t1 <- getCurrentTime
    let c= matrixproduct a b
    t2 <- getCurrentTime
    putStrLn $ show $ diffUTCTime t2 t1
    print $ sum [sum x | x<-c]