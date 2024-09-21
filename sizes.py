import os

def find_sizes(original , compressed):
        org_files = set(os.listdir(original))
        comp_files = set(os.listdir(compressed))
        common_files = org_files.intersection(comp_files)
        size_differences = []
        
        for filename in common_files:
                path1 = os.path.join(original, filename)
                path2 = os.path.join(compressed, filename)
                
                size1 = os.path.getsize(path1)
                size2 = os.path.getsize(path2)
                
                size_difference = abs(size1 - size2)
                size_differences.append(size_difference)

        if size_differences:
                min_diff = min(size_differences)
                max_diff = max(size_differences)
        
        return [min_diff , max_diff]