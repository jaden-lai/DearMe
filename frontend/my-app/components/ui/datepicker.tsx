"use client"

import * as React from "react"
import { format } from "date-fns"
import { Calendar as CalendarIcon } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"

export function DatePickerDemo({ onDateChange }) {
  const [date, setDate] = React.useState<Date>()

  const handleSubmit = () => {
    if (date) {
      // console.log("Selected date:", date);

      // Format the date to be YYYYMMDD
      const session = format(date, "yyyyMMdd");
      console.log("Formatted date:", session);
      setDate(date);
      onDateChange(session);
    }
  };

  return (
    <div className="flex flex-col gap-2">
      <Popover>
        <PopoverTrigger asChild>
          <Button
            variant={"outline"}
            className={cn(
              "w-[280px] justify-start text-left font-normal bg-slate-950 text-white border-gray-700",
              !date && "text-gray-400"
            )}
          >
            <CalendarIcon className="mr-2 h-4 w-4" />
            {date ? format(date, "PPP") : <span>View past entries</span>}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0 bg-slate-950 border-gray-700">
          <Calendar
            mode="single"
            selected={date}
            onSelect={setDate}
            initialFocus
            className="bg-slate-950 text-white"
          />
        </PopoverContent>
      </Popover>

      <Button 
        onClick={handleSubmit}
        disabled={!date}
        variant={"outline"}
        className={cn(
          "w-[280px] justify-start text-left font-normal bg-slate-950 text-white border-gray-700 hover:bg-slate-900",
          !date && "text-gray-400"
        )}
      >
        Search date
      </Button>
    </div>
  )
}
