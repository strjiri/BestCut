from typing import List, Dict, Tuple
import dataclasses


@dataclasses.dataclass
class Length:
	length:int
	id:int


@dataclasses.dataclass
class Ordered_Stock:
	length:int
	count:int

	def take(self)->int: 
		if self.count>0: 
			self.count -= 1
			return self.length
		return 0
	
	
	

class NotEnoughStockItems(Exception): pass
		

def mincutsort(lengths_list:List[int],stock_dict:Dict[int,int])->Tuple[List[Length],List[int]]:
	# The lengths list is converted into list of Length objects, which keep their original id
	# stored as an attribute for later use.
	__check_enough_stock_items(sum(lengths_list),stock_dict)

	lengths:List[Length] = __prepare_lengths_for_sorting(lengths_list)
	stock:List[Ordered_Stock] = __prepare_stock_for_taking(stock_dict)

	matching_lengths = __pick_lengths_and_stock_of_same_length(lengths,stock)
	remaining_sorted_lengths, remaning_sorted_stock = __sort_unmatching_stock_and_lengths(lengths,stock)
	sorted_lengths = matching_lengths.copy() + remaining_sorted_lengths
	sorted_stock = [l.length for l in matching_lengths] + remaning_sorted_stock

	return sorted_lengths, sorted_stock


def __check_enough_stock_items(total_length, stock:Dict[int,int]):
	stock_length_sum = 0
	for length,count in stock.items(): stock_length_sum += length*count
	if stock_length_sum<total_length: raise NotEnoughStockItems
	

def __prepare_lengths_for_sorting(lengths:List[int])->List[Length]:
	return [Length(lengths[i],i) for i in range(len(lengths))]

def __prepare_stock_for_taking(stock:Dict[int,int])->List[Ordered_Stock]:
	ordered_stock:List[Ordered_Stock] = list()
	for length,count in stock.items():
		ordered_stock.append(Ordered_Stock(length,count))
	return ordered_stock


def __pick_lengths_and_stock_of_same_length(
	lengths:List[Length],
	stock:List[Ordered_Stock]
	)->List[Length]:

	matches:List[Length] = list()
	for stock_item in stock:
		for length_item in lengths:
			if (stock_item.length==length_item.length) and (stock_item.take()>0): 
				lengths.remove(length_item)
				matches.append(length_item)
	return matches


def __sort_unmatching_stock_and_lengths(
	lengths:List[Length],
	stock:List[Ordered_Stock]
	)->Tuple[List[Length],List[int]]:

	sorted_stock:List[int] = list()
	sorted_lengths:List[Length] = lengths.copy()

	stock_length_sum = __sum_ordered_stock_lengths(stock)
	lengths_sum = __sum_lengths(lengths)
	
	sorted_lengths, sorted_stock = \
		_maximize_matching_ends(lengths_sum,stock_length_sum,lengths,stock)

	return sorted_lengths, sorted_stock


_memo:Dict[str,Tuple[List[Length],List[int]]] = dict()
def _maximize_matching_ends(
	length_sum:int, 
	stock_length_sum:int, 
	lengths:List[Length], 
	stock:List[Ordered_Stock]
	)->Tuple[List[Length],List[int]]:

	sorted_stock:List[int] = list()
	k = 0
	while k<len(stock):
		taken_item_length = stock[k].take()
		if taken_item_length==0: 
			k+=1
			continue
		else:
			sorted_stock.append(taken_item_length)

	return lengths.copy(), sorted_stock.copy()


def __sum_ordered_stock_lengths(stock:List[Ordered_Stock]):
	stock_length_sum = 0
	for item in stock: stock_length_sum += item.count*item.length
	return stock_length_sum

def __sum_lengths(lengths:List[Length]):
	lengths_sum = 0
	for item in lengths: lengths_sum += item.length
	return lengths_sum




