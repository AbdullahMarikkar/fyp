import { useQuery } from "@tanstack/react-query";
import { getHistory } from "../uploadImages";

export function useGetHistory() {
  const {
    refetch,
    isLoading,
    data: history,
    error,
  } = useQuery({
    queryKey: ["history"],
    queryFn: getHistory,
  });

  return { isLoading, error, history, refetch };
}
