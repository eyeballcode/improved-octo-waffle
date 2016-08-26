class List():
    def __init__(self, *args, **kwargs):
        if 'array' in kwargs:
            if isinstance(kwargs.get('array'), list):
                self.array = kwargs.get('array')
            else:
                raise Exception('Passed array is not an array')
        elif 'length' in kwargs:
            self.array = [None for i in range(kwargs.get('length'))]
            return
        else:
            self.array = []
        for item in kwargs:
            if item != 'array':
                self.array.append(item)
        for item in args:
            self.array.append(item)

    def __repr__(self):
        return str(self.array)

    def get_array(self):
        return self.array
    
    def get_item(self, index):
        if isinstance(index, int):
            if index > len(self.array):
                return (None)
            else:
                return self.array[index]
        if isinstance(index, str):
            index = index.replace(' ', '')
            data_segments = []
            read_so_far = ''
            last_colon_pos = 0
            if list(index).count(':') > 2:
                raise Exception('That is not a slice string (' + index + ') (Too many colons)') 
            for char in index:
                if (char != ':' and char != '-' and not char.isdigit()) or len(data_segments) + 1 > 3:
                    raise Exception('That is not a slice string (' + index + ')\n' + 
                                    '                                       ' + ''.join([' ' for i in read_so_far]) + '^')
                if char == ':':
                    data_segments.append(read_so_far[last_colon_pos:len(read_so_far)])
                    last_colon_pos = len(read_so_far) + 1
                elif len(read_so_far) + 1 == len(index):
                    data_segments.append(index[last_colon_pos:])
                read_so_far += char
            if last_colon_pos == 0:
                return self.array[int(index)]
            data_segments = map(lambda x: None if x == '' else x, data_segments)
            data_segments = list(map(lambda x: None if x == None else int(x), data_segments))
            data_segments += [None for i in range(3 - len(data_segments))]
            return self.array[data_segments[0]:data_segments[1]:data_segments[2]]
 
    def swap(self, first, second):
        temp = self.array[first]
        self.array[first] = self.array[second]
        self.array[second] = temp
        return self
  
    def remove(self, index):
        if len(self.array) > index:
            self.array.pop(index)  
        return self

    def add(self, item, *args):
        index = len(self.array) if len(args) < 1 else args[0]
        self.array[index:index] = [item]
        return self

    def reverse(self):
        self.array = self.array[::-1]
        return self

    def move(self, start, end, new_index):
        before = self.array[0:start]
        after = self.array[end:]
        move = self.array[start:end]
        self.array = before + after + move
        return self

    def map(self, function):
        self.array = list(map(function, self.array))
        return self

    def filter(self, function):
        self.array = list(filter(function, self.array))
        return self

    def reduce(self, function, *args):
        initializer = 0 if len(args) < 1 else args[0]
        if 'reduce' not in globals():
            from functools import reduce
        return reduce(function, self.array, initializer)
