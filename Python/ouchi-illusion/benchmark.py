import ouchi, time, argparse
from math import sqrt

def eval(values):
    average = sum(values) / len(values)
    variance = 0
    for val in values:
        variance += (val - average)**2
    variance /= len(values)
    derivation = sqrt(variance)
    return average, derivation, variance



def benchmark(sample_size, image_size_power, mode):
    print("=== BENCHMARK ===")
    print(f"Runs: {sample_size}, Image size: {2 ** image_size_power}")

    pad_size = len(str(sample_size))
    if mode is None:
        result = []
        for i in range(3):
            result.append([])
            for j in range(1, sample_size + 1):
                print(f"Mode: {i + 1}, Run: {str(j).zfill(pad_size)}", end="\r")
                t = time.time()
                ouchi.create_image(i, 2 ** image_size_power)
                result[i].append(time.time() - t)

        print("Average time and standard derivation in seconds:")
        for i in range(len(result)):
            avg, sderiv, var = eval(result[i])
            print(f"- Mode {i + 1}:\n{' '*4}Ø  {avg}\n"
                f"{' '*4}σ  {sderiv}\n{' '*4}σ² {var}")
    else:
        result = []
        for j in range(1, sample_size + 1):
                print(f"Mode: {mode}, Run: {str(j).zfill(pad_size)}", end="\r")
                t = time.time()
                ouchi.create_image(mode, 2 ** image_size_power)
                result.append(time.time() - t)
        avg, sderiv, var = eval(result)
        print("Average time and standard derivation in seconds:")
        print(f"- Mode {mode}:\n{' '*4}Ø  {avg}\n"
                f"{' '*4}σ  {sderiv}\n{' '*4}σ² {var}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark for Ouchi Illusion Modes")
    parser.add_argument("-r", "--runs", action="store", type=int, nargs="?",
        default=100, help="number of test runs (min: 1, default: 100)")
    parser.add_argument("-e", "--exponent", action="store", type=int, nargs="?",
        default=9, help="exponent for the image size as power of two (min: 7, default: 9)")
    parser.add_argument("-m", "--mode", action="store", type=int, nargs="?",
        default=None, help="processing mode to be tested (1, 2 or 3) (optional)")

    p = parser.parse_args()
    if p.runs < 1:
        parser.error("Minimum number of runs is 1")
    if p.exponent < 7:
        parser.error("Minimum exponent is 7")
    if p.mode is not None and p.mode not in [1, 2, 3]:
        parser.error("Mode has to be 1, 2 or 3")
        
    benchmark(p.runs, p.exponent, p.mode)